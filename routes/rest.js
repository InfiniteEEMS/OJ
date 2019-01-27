const express = require('express');
const router = express.Router();

// request body is json format, json parser is used to parse the body
const bodyParser = require('body-parser');
const jsonParser = bodyParser.json();

const problemService = require('../services/problemService');

const nodeRestClient = require('node-rest-client').Client;
const restClient = new nodeRestClient();

EXECUTOR_SERVER_URL = 'http://localhost:5000/build_and_run';
restClient.registerMethod('build_and_run', EXECUTOR_SERVER_URL, 'POST');

//GET all problems
router.get('/problems', (req, res) => {
    problemService.getProblems()
      .then(problems => res.json(problems));
});

//GET problem by id
router.get('/problems/:id', (req, res) => {
    const id = req.params.id;
    problemService.getProblem(+id)
      .then(problem => res.json(problem));
});

//POST new problem
router.post('/problems', jsonParser, (req, res) => {
  problemService.addProblem(req.body)
    .then(problem => res.json(problem), 
     error => res.status(400).send("Problem name already exists!")
  );
});

// build and run problem
router.post('/build_and_run', jsonParser, (req, res) => {

  console.log("Got a call to /test");
  console.log("code:" + req.body.code);
  console.log("lang:" + req.body.lang); 
  console.log("id:" + req.body.id)

  const args = {data: { code:req.body.code, lang:req.body.lang, id:req.body.id },
                headers: {'Content-Type': 'application/json'}};
  
  restClient.methods.build_and_run(
    args,
    (data, response) => {
      const status = `Build status: ${data['status']}`;
      console.log(status);
      res.json(data);
    }
  );
});

// edit problem
router.put('/problems', jsonParser, (req, res) => {
  problemService.editProblem(req.body)
    .then(problem => res.json(problem),
     error => res.status(400).send("Failed to update problem"));
});

//test
router.post('/test', jsonParser, (req, res) => {
    res.json(req.body);
});

module.exports = router;
