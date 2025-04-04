package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type Classification struct {
	ID   uint   `gorm:"primaryKey"`
	Name string `gorm:"not null;unique"`
}

type History struct {
	ID               uint   `gorm:"primaryKey"`
	UserName         string `gorm:"not null"`
	Query            string `gorm:"not null"`
	ClassificationId *int   `gorm:"null"`
	Responce         string `gorm:"null"`
	Rating           *int   `gorm:"null"`
}

var db *gorm.DB

func initDB() {
	dsn := "host=localhost user=postgres password=Qwerty11 dbname=tenderhack port=5432 sslmode=disable"
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
	r.PUT("/history/:id", updateHistory)
	r.DELETE("/history/:id", deleteHistory)
	r.GET("/history", getHistory)

	r.Run(":8080")
}

func createHistory(c *gin.Context) {
	var history History
	if err := c.ShouldBindJSON(&history); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := db.Create(&history).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, history)
}

func updateHistory(c *gin.Context) {
	var history History

	// Bind JSON data.
	if err := c.ShouldBindJSON(&history); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Find the history by ID and update.
	if err := db.Model(&History{}).Where("id = ?", c.Param("id")).Updates(&history).Error; err != nil {
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
	fmt.Print(history)
	c.JSON(http.StatusOK, history)
}
