package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

func main() {
	data, err := os.ReadFile("./urls.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(data), "\r\n")

	var failed []string

	for _, line := range lines {
		b := download_file(line)
		if !b {
			failed = append(failed, line)
		}
	}

	fmt.Println("下载失败的文件：", failed)
}

func download_file(url string) bool {
	path := url[30:]
	pos := strings.LastIndex(path, "/")
	dir := path[:pos]

	os.MkdirAll(dir, 0750)

	rsp, err := http.Get(url)
	if err != nil {
		fmt.Println("http.Get error:", url, err)
		return false
	}

	defer rsp.Body.Close()

	f, err := os.Create(path)
	if err != nil {
		fmt.Println("os.Create error:", path, err)
		return false
	}

	defer f.Close()

	io.Copy(f, rsp.Body)

	return true
}
