package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"sync/atomic"
	"time"
)

const STARTURL string = "http://www.mzitu.com/japan" //妹子图模块列表页url

var (
	total int32
	gets  int32
)

func main() {
	getPage(STARTURL)
	fmt.Println("complete !!!")
}

//下载html
func getHtml(url string) (succ bool, html string) {
	response, err := http.Get(url)
	if err != nil {
		return
	}
	defer response.Body.Close()

	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return
	}
	succ = true
	html = string(body)
	return
}

//获取最大分页
func getPage(url string) (page int) {
	fmt.Println(url, "Starting...")
	succ, html := getHtml(url)
	if !succ {
		return
	}

	reg, err := regexp.Compile("http://www.mzitu.com/([0-9]+)")
	if err != nil {
		return
	}

	set := reg.FindAllStringSubmatch(html, 200)

	fmt.Println("共", len(set), "页")
	page = len(set)

	for _, v := range set {
		download(v[0], v[1])
	}

	for {
		if total == gets {
			break
		}
		time.Sleep(1 * time.Second)
	}
	return
}

//下载图片
func download(url string, page string) {

	for i := 1; i < 100; i++ {

		newurl := url + "/" + strconv.Itoa(i)

		succ, html := getHtml(newurl)
		if !succ {
			return
		}

		reg, _ := regexp.Compile("main-image.*(http://i.meizitu.net.*.jpg)")
		iterms := reg.FindAllStringSubmatch(html, 100)

		atomic.AddInt32(&total, int32(len(iterms)))

		for _, vv := range iterms {
			go SaveImage(newurl, vv[1], page, i)
		}

	}

}

func SaveImage(url string, img string, page string, idx int) bool {
	defer atomic.AddInt32(&gets, 1)
	// defer fmt.Println("download image: ", url, img, " OK !!!")
	fmt.Println("download image: ", img)

	res, err := http.Get(img)
	if err != nil {
		fmt.Printf("%d HTTP ERROR:%s", err)
		return false
	}
	defer res.Body.Close()

	//根据URL文件名创建文件
	filename := page + "_" + strconv.Itoa(idx) + ".jpg"
	dst, err := os.Create(filename)
	if err != nil {
		fmt.Println("%d HTTP ERROR:%s", err, dst)
		return false
	}
	dst.Close()

	// 写入文件
	io.Copy(dst, res.Body)

	return true
}
