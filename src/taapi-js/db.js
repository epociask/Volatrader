const knex = require('knex')

const db = knex({
  client: 'pg',
  connection: {
    host : 'coin-do-user-7113675-0.db.ondigitalocean.com',
    user : 'postgres',
    port : 25060,
    database : 'defaultdb',
    password: 'imt6kws2bm7ffay8',
  },
});

module.exports = db