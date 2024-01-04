package main

import (
	"encoding/csv"
	"fmt"
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
	header := []string{"Timestamp", "Jméno Aplikace", "Log Záznam"}
	err = writer.Write(header)
	if err != nil {
		fmt.Println("Chyba při zápisu hlavičky:", err)
		return
	}

	// Generování náhodných dat pro dataset
	for i := 1; i <= 10; i++ {
		timestamp := time.Now().Unix()
		appName := fmt.Sprintf("Aplikace %d", i)
		logRecord := fmt.Sprintf("Log záznam pro aplikaci %d", i)

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
