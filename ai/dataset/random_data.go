package main

import (
	"encoding/csv"
	"fmt"
	"math/rand"
	"os"
	"time"
)

func main() {
	// Nastavení názvu souboru CSV
	fileName := "dataset.csv"

	// Otevření souboru pro zápis
	file, err := os.Create(fileName)
	if err != nil {
		fmt.Println("Chyba při vytváření souboru:", err)
		return
	}
	defer file.Close()

	// Vytvoření objektu CSV writeru
	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Zápis hlavičky CSV souboru
	header := []string{"Timestamp", "AppName", "Log"}
	err = writer.Write(header)
	if err != nil {
		fmt.Println("Chyba při zápisu hlavičky:", err)
		return
	}

	// Seznam názvů aplikací
	appNames := []string{"Aplikace1", "Aplikace2", "Aplikace3"}

	// Generování náhodných dat pro dataset
	for i := 1; i <= 10000; i++ {
		timestamp := time.Now().Unix()
		appName := getRandomAppName(appNames)
		logRecord := getRandomLogRecord()

		// Vytvoření řádku dat
		row := []string{fmt.Sprint(timestamp), appName, logRecord}

		// Zápis dat do CSV souboru
		err := writer.Write(row)
		if err != nil {
			fmt.Println("Chyba při zápisu dat:", err)
			return
		}
	}

	fmt.Println("Dataset byl úspěšně vytvořen v souboru:", fileName)
}

// Funkce pro získání náhodného názvu aplikace
func getRandomAppName(appNames []string) string {
	// Náhodný výběr názvu aplikace
	return appNames[rand.Intn(len(appNames))]
}

// Funkce pro získání náhodného log záznamu
func getRandomLogRecord() string {
	// Seznam možných log záznamů
	logRecords := []string{"Connection Success", "Connection Timeout"}

	// Náhodný výběr log záznamu
	return logRecords[rand.Intn(len(logRecords))]
}
