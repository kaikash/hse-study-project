const http = require('http')
const Koa = require('koa')
const Router = require('@koa/router')
const bodyParser = require('koa-bodyparser')
const fs = require('fs')
const xmlrpc = require('xmlrpc')

const app = new Koa()
const router = new Router()

var client = xmlrpc.createClient({ host: 'localhost', port: 9090, path: '/'})
 
function methodCall(...args) {
    return new Promise((resolve, reject) => {
        client.methodCall(...args, function (error, value) {
            if (error) return reject(error)
            resolve(value)
        })
    })
}

const UPLOADS_DIR = __dirname + '/data'

router.post('/predict', async (ctx, next) => {
    try {
        let filename = `${Math.floor(Math.random() * 1000 * 1000 * 1000 * 1000 * 1000 * 1000).toString(32)}.json`
        let fileabspath = `${UPLOADS_DIR}/${filename}`
        fs.writeFileSync(fileabspath, JSON.stringify(ctx.request.body))
        let res = await methodCall('predict', [fileabspath])
        res = res.reduce((acc, [value, name]) => ({ [name]: value, ...acc }), {})
        ctx.body = { result: res }
    } catch (err) {
        ctx.status = 500
        ctx.body = { error: err.message }
    }
})

app
.use(bodyParser())
.use(router.routes())
.use(router.allowedMethods())

http.createServer(app.callback()).listen(3007)
