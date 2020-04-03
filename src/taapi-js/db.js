const knex = require('knex')

const db = knex({
  client: 'pg',
  connection: {
    host : 'production-do-user-7113675-0.a.db.ondigitalocean.com',
    user : 'postgres',
    port : 25060,
    database : 'defaultdb',
    password: 'imt6kws2bm7ffay8',
  },
});

module.exports = db