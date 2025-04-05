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
)

const configPath = "config.yml"

type Classification struct {
	ID   uint   `gorm:"primaryKey"`
	Name string `gorm:"not null;unique"`
}

type History struct {
	ID               uint      `gorm:"primaryKey,dbname(id)"`
	UserUuid         uuid.UUID `gorm:"not null"`
	Query            string    `gorm:"not null"`
	ClassificationId *int      `gorm:"null"`
	Responce         *string   `gorm:"null"`
	Rating           *int      `gorm:"null"`
	DateTimeCreate   time.Time `gorm:"not null"`
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
	db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
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
	r.PUT("/history/Rating", updateHistoryRating)
	r.DELETE("/history/:id", deleteHistory)
	r.GET("/history", getHistory)
	r.GET("/historyUser/:UserUuid", getHistoryUser)

	r.POST("/classification", createClassification)
	r.GET("/classification", getClassification)

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
