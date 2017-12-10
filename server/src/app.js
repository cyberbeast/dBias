const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const morgan = require('morgan');
const socketio = require('socket.io');
const mongoose = require('mongoose');
const config = require('./config');
const Task = require('./models/task');
mongoose.connect(config.dbURI, { useMongoClient: true });

const app = express();
app.use(morgan('combined'));
app.use(bodyParser.json());
app.use(cors());

app.get('/posts', (req, res) => {
	res.send([
		{
			title: 'Hello World!',
			description: 'Hi there! How are you?'
		}
	]);
});

var server = app.listen(process.env.PORT || 8081, function() {
	console.log('Server listening on *:8081');
});

var io = socketio(server);
var supervisorConfiguration = {
	active: false
};

io.on('connection', function(socket) {
	console.log('a user connected');

	socket.on('disconnect', function() {
		console.log('user disconnected');
	});

	socket.on('getDatasets', function() {
		console.log('Client requesting for available datasets');
		var sampleDatasetList = [
			{
				name: 'Sample',
				description: 'Nice Description',
				features: ['age', 'race'],
				rows: 20
			},
			{
				name: 'Sample2',
				description: 'Nice Description2',
				features: ['age2', 'race2'],
				rows: 220
			}
		];
		socket.send({
			event: 'RES:getDatasets',
			data: sampleDatasetList
		});
	});

	socket.on('getSupervisorConfiguration', function() {
		console.log('Supervisor Client requesting for Supervisor Configuration');
		socket.send({
			event: 'RES:getSupervisorConfiguration',
			data: supervisorConfiguration
		});
	});

	socket.on('toggleSupervisor', function() {
		supervisorConfiguration.active = supervisorConfiguration.active == true ? false : true;
		console.log('Supervisor Client is requesting to toggle state!', supervisorConfiguration.active);
		socket.send({
			event: 'RES:toggleSupervisor',
			data: supervisorConfiguration
		});
	});

	socket.on('newTask', function(params) {
		var tempTask = new Task(params);
		tempTask.save(function(err, temp) {
			if (err) console.log('Error while creating new task template. ', err);

			Task.findById(temp.id, function(err, task) {
				if (err) console.log('Error while retrieving the newly created task template. ', err);
				console.log('Sending... ', task);
				socket.send({ event: 'RES:newTask', data: task });
			});
		});
	});

	socket.on('getTasks', function() {
		console.log('Client requesting for Current System Tasks');
		Task.find({}, function(err, tasks) {
			if (err) throw err;

			socket.send({ event: 'RES:getTasks', data: tasks });
		});
	});

	socket.on('trainTaskByID', function(id) {
		console.log('Client requesting trainTaskByID on: ', id);
	});
});
