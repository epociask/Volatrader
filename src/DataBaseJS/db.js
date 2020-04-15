const knex = require('knex')

const { DATABASE_NAME } = process.env

const db = knex({
  client: 'pg',
  connection: {
    host : 'production-do-user-7113675-0.a.db.ondigitalocean.com',
    user : 'doadmin',
    port : 25060,
    database : 'defaultdb',
    password: 'lddq4pu1lwmyviis',
    ssl: true,
  },
});

const localdb = knex({
  client: 'pg',
  connection: {
    host: '127.0.0.1',
    port: 5432,
    database: 'coin-database',
    password: '',
    user: 'postgres'
  }
})

console.log(DATABASE_NAME)

module.exports = DATABASE_NAME == 'PRODUCTION' ? db : localdb


// username = doadmin
// password = lddq4pu1lwmyviis hide
// host = production-do-user-7113675-0.a.db.ondigitalocean.com
// port = 25060
// database = defaultdb
// sslmode = require