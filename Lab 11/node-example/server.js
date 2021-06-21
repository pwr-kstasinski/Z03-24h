const express = require("express");
const mariadb = require("mariadb");

const app = express();
const port = 5000;

const pool = mariadb.createPool({
  host: process.env['DB_HOST'],
  user: process.env['DB_USER'],
  password: process.env['DB_PASS'],
  connectionLimit: 5,
  database: process.env['DB_DEFAULT'],
});

let isHealthy = true;
app.get("/healthcheck", (req, res) => {
    console.log(`healthcheck: ${isHealthy}`);
    
    if(isHealthy) {
        res.sendStatus(200)
    } else {
        res.sendStatus(500)
    }
})

app.get("/set-unhealthy", (req, res) => {
    isHealthy = false;
    res.send("unhealthy")
})

app.get("/", (req, res) => {
  console.log(`Got request with query: ${JSON.stringify(req.query)}`);

  if (req.query["message"]) {
    pool
      .getConnection()
      .then((conn) => {
        conn
          .query("SELECT 1 as val")
          .then((rows) => {
            console.log(rows); //[ {val: 1}, meta: ... ]
            //Table must have been created before
            // " CREATE TABLE myTable (id int, val varchar(255)) "
            return conn.query("INSERT INTO myTable value (?, ?)", [
              1,
              req.query["message"],
            ]);
          })
          .then((response) => {
            console.log(response); // { affectedRows: 1, insertId: 1, warningStatus: 0 }
            conn.end();

            res.send("Message added!");
          })
          .catch((err) => {
            //handle error
            console.log(err);
            conn.end();

            res.send(`Error while adding messages! ${err}`);
          });
      })
      .catch((err) => {
        //not connected
        res.send(`Error while adding messages! ${err}`);
      });
  } else {
    pool
    .getConnection()
    .then((conn) => {
      conn
        .query("SELECT * FROM myTable")
        .then((rows) => {
          console.log(rows);
          res.send(rows);
        })
        .catch((err) => {
          //handle error
          console.log(err);
          conn.end();

          res.send(`Error while adding messages! ${err}`);
        });
    })
    .catch((err) => {
      res.send(`Error while adding messages! ${err}`);
    });
  }
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
