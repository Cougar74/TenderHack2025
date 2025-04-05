package main

import (
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/gofrs/uuid/v5"
	"gopkg.in/yaml.v3"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

const configPath = "config.yml"

type Classification struct {
	ID   int    `gorm:"primaryKey; column:id"`
	Name string `gorm:"not null;unique; column:name"`
}

func (Classification) TableName() string {
	return "classifications"
}

type History struct {
	ID               int       `gorm:"primaryKey; column:id"`
	UserUuid         uuid.UUID `gorm:"not null; column:user_uuid"`
	Query            string    `gorm:"not null; column:query"`
	ClassificationId *int      `gorm:"null; column:classification_id"`
	Responce         *string   `gorm:"null; column:responce"`
	Rating           *int      `gorm:"null; column:rating"`
	DateTimeCreate   time.Time `gorm:"not null; column:date_time_create"`
}

func (History) TableName() string {
	return "histories"
}

type CategoriesByDate struct {
	ClassificationName string    `gorm:"null; column:classification_name"`
	InteractionResult  string    `gorm:"null; column:interaction_result"`
	DateCreate         time.Time `gorm:"null; column:date_create"`
	Count              int       `gorm:"not null; column:count"`
}

func (CategoriesByDate) TableName() string {
	return "сategories_by_date"
}

type HistoryCreate struct {
	UserUuid uuid.UUID
	Query    string
}

type HistoryUpdateResponceAndClassificationId struct {
	ID               uint
	Responce         *string
	ClassificationId *int
}

type HistoryUpdateResponceAndClassificationName struct {
	ID                 uint
	Responce           *string
	ClassificationName string
}
type HistoryUpdateRating struct {
	ID     uint
	Rating *int
}

var db *gorm.DB

type Cfg struct {
	DB   string `yaml:"db"`
	HOST string `yaml:"host"`
}

var AppConfig *Cfg

func ReadConfig() {
	f, err := os.Open(configPath)
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	decoder := yaml.NewDecoder(f)

	err = decoder.Decode(&AppConfig)
	if err != nil {
		fmt.Println(err)
	}
}

func initDB() {
	ReadConfig()
	dsn := AppConfig.DB
	var err error
	db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	})

	if err != nil {
		panic("failed to connect to database")
	}

	//db.AutoMigrate(&Classification{})
	//db.AutoMigrate(&History{})
}

func main() {
	initDB()
	r := gin.Default()

	r.POST("/history", createHistory)
	r.PUT("/history/ResponceAndClassificationId", updateHistoryResponceAndClassificationId)
	r.PUT("/history/ResponceAndClassificationName", updateHistoryResponceAndClassificationName)
	r.PUT("/history/Rating", updateHistoryRating)
	r.DELETE("/history/:id", deleteHistory)
	r.GET("/history", getHistory)
	r.GET("/historyUser/:UserUuid", getHistoryUser)

	r.POST("/classification", createClassification)
	r.GET("/classification", getClassification)

	r.GET("/categoriesbydate", getCategoriesByDate)

	r.Run(AppConfig.HOST)
}

func createHistory(c *gin.Context) {
	var historyCreate HistoryCreate

	if err := c.ShouldBindJSON(&historyCreate); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var history = History{
		UserUuid:         historyCreate.UserUuid,
		Query:            historyCreate.Query,
		ClassificationId: nil,
		Responce:         nil,
		Rating:           nil,
		DateTimeCreate:   time.Now(),
	}

	if err := db.Create(&history).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, history.ID)
}

func updateHistoryResponceAndClassificationId(c *gin.Context) {
	var historyUpdate HistoryUpdateResponceAndClassificationId

	// Bind JSON data.
	if err := c.ShouldBindJSON(&historyUpdate); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var historyNew = History{
		Responce:         historyUpdate.Responce,
		ClassificationId: historyUpdate.ClassificationId,
	}
	// Find the history by ID and update.
	if err := db.Model(&History{}).Where("id = ?", historyUpdate.ID).Updates(&historyNew).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "history updated successfully"})
}
func updateHistoryResponceAndClassificationName(c *gin.Context) {
	var historyUpdate HistoryUpdateResponceAndClassificationName

	// Bind JSON data.
	if err := c.ShouldBindJSON(&historyUpdate); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var classification = Classification{Name: historyUpdate.ClassificationName}

	// Find the history by ID and update.
	if err := db.
		Where(&Classification{Name: historyUpdate.ClassificationName}).
		Find(&classification).
		Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	var historyNew = History{
		Responce:         historyUpdate.Responce,
		ClassificationId: &classification.ID,
	}
	// Find the history by ID and update.
	if err := db.Model(&History{}).Where("id = ?", historyUpdate.ID).Updates(&historyNew).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": fmt.Sprintf("%s%d%s%s", "history updated successfully ClassificationID = ", classification.ID, ", ClassificationName = ", historyUpdate.ClassificationName)})
}

func updateHistoryRating(c *gin.Context) {
	var historyUpdate HistoryUpdateRating

	// Bind JSON data.
	if err := c.ShouldBindJSON(&historyUpdate); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var historyNew = History{
		Rating: historyUpdate.Rating,
	}
	// Find the history by ID and update.
	if err := db.Model(&History{}).Where("id = ?", historyUpdate.ID).Updates(&historyNew).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "history updated successfully"})
}

func deleteHistory(c *gin.Context) {
	if err := db.Delete(&History{}, c.Param("id")).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "history deleted successfully"})
}

func getHistory(c *gin.Context) {
	var history []History
	db.Find(&history)
	c.JSON(http.StatusOK, history)
}

func getHistoryUser(c *gin.Context) {
	var history []History
	//var uuid = uuid.Must(uuid.FromString(c.Param("UserUuid")))
	db.Where("user_uuid = ?", c.Param("UserUuid")).Find(&history)
	c.JSON(http.StatusOK, history)
}

func createClassification(c *gin.Context) {
	var classification Classification
	if err := c.ShouldBindJSON(&classification); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := db.Create(&classification).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, classification)
}

func getClassification(c *gin.Context) {
	var classification []Classification
	db.Find(&classification)
	c.JSON(http.StatusOK, classification)
}

func getCategoriesByDate(c *gin.Context) {
	var categoriesByDate []CategoriesByDate
	db.Find(&categoriesByDate)
	c.JSON(http.StatusOK, categoriesByDate)
}
