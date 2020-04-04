const knex = require('knex')

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


module.exports = db


// username = doadmin
// password = lddq4pu1lwmyviis hide
// host = production-do-user-7113675-0.a.db.ondigitalocean.com
// port = 25060
// database = defaultdb
// sslmode = require