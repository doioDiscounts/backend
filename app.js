const express = require('express')
const cors = require('cors')
const { Client } = require('@elastic/elasticsearch')
const helmet = require("helmet")
const fs = require('fs');
require("dotenv").config()

const { dummyData } = require("./dummyData")

const app = express()

const elasticSearchClient = new Client({ node: process.env.ELASTICSEARCH_URL })

app.use(express.json())
app.use(cors())
app.use(helmet())

let paginate = (data, items, pageNumber) => {
    if (items > 49 || items < 1) { items = 50 }
    let beggining = (items * pageNumber) - items
    let end = beggining + items
    return { data: data.slice(beggining, end), previousPage: data[beggining - 1], forwardPage: data[end] }
}

app.post('/getProducts', async (req, res) => {
    // let results = await elasticSearchClient.search({
    //     index: 'products',
    //     body: req.body.query,
    //     size: 10000
    // })
    // let response = paginate(results.body.hits.hits, req.body.items, req.body.pageNumber)
    let response = paginate(dummyData, req.body.items, req.body.pageNumber)
    res.send(response)
})

// Get categories from all products and append them to file 
app.get('/getCategories', async (req, res) => {
    const categories = await elasticSearchClient.search({
        index: 'products',
        body: { query: { match_all: {} } },
        size: 10000
    })
    let categoryList = []
    for (const category of categories.body.hits.hits) {
        if (!categoryList.includes(category._source.category)) {
            categoryList.push(category._source.category)
        }
    }
    fs.writeFile('categories.json', JSON.stringify(categoryList), (r) => { })
    res.send(categoryList)
})

// Send categories to frontend 
app.get('/sendCategories', async (req, res) => {
    fs.readFile('categories.json', (e, data) => {
        res.send(JSON.parse(data.toString()))
    })
})

// 
app.post('/sendClickInfo', async (req, res) => {
    await elasticSearchClient.updateByQuery({
        index: 'clicks',
        refresh: true,
        body: {
            script: {
                lang: 'painless',
                source: 'ctx._source.clicks += params.count',
                params: { count: 1 }
            },
            query: {
                match: {
                    provider: req.body.productProvider
                }
            }
        }
    })
    res.send('')
})

app.listen(3001)