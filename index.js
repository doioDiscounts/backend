const express = require('express')
const cors = require('cors')
const { Client } = require('@elastic/elasticsearch')
const helmet = require("helmet")
require("dotenv").config()
const dummyProducts = require('./dummyData/dummyProducts.json')
const dummyCategories = require('./dummyData/dummyCategories.json')
const dummyScore = require('./dummyData/dummyScore.json')

const app = express()

const elasticSearchClient = new Client({ node: process.env.ELASTICSEARCH_URL })

app.use(express.json())
app.use(cors())
app.use(helmet())

const paginate = (data, items, pageNumber) => {
    if (items > 49 || items < 1) { items = 50 }
    let beggining = (items * pageNumber) - items
    let end = beggining + items
    return {
        data: data.slice(beggining, end),
        previousPage: data[beggining - 1] ? true : false,
        forwardPage: data[end] ? true : false
    }
}

app.post('/getProducts', async (req, res) => {
    // let query
    // if (req.body.searchItem) {
    //     query = {
    //         "query": {
    //             "bool": {
    //                 "should": [
    //                     {
    //                         "match": {
    //                             "title": {
    //                                 "query": req.body.searchItem,
    //                                 "fuzziness": "AUTO"
    //                             }
    //                         }
    //                     },
    //                     {
    //                         "match": {
    //                             "category": {
    //                                 "query": req.body.searchItem,
    //                                 "fuzziness": "AUTO"
    //                             }
    //                         }
    //                     }
    //                 ]
    //             }
    //         }
    //     }
    // }

    // let results = await elasticSearchClient.search({
    //     index: 'products',
    //     body: query,
    //     size: 10000
    // })
    // let response = paginate(results.body.hits.hits, req.body.items, req.body.pageNumber)
    // res.send(response)
    res.send(paginate(dummyProducts, req.body.items, req.body.pageNumber))
})

app.get('/getCategories', async (req, res) => {
    // const categories = await elasticSearchClient.search({
    //     index: 'categories'
    // })
    // res.send(categories.body.hits.hits[0]._source.categories)
    res.send(dummyCategories)
})

app.post('/sendClickInfo', async (req, res) => {
    // await elasticSearchClient.updateByQuery({
    //     index: 'providers',
    //     refresh: true,
    //     body: {
    //         script: {
    //             lang: 'painless',
    //             source: 'ctx._source["count"] += 1'
    //         },
    //         query: {
    //             match: {
    //                 provider: req.body.provider
    //             }
    //         }
    //     }
    // })
    // res.send('')
    for (const provider of dummyScore.providers) {
        if (provider.provider == req.body.provider) {
            provider.count += 1
        }
    }
    console.log(dummyScore)
    res.send('')
})

app.listen(3001)