const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const morgan = require('morgan');
const socketio = require('socket.io');
const mongoose = require('mongoose');
const config = require('./config');
const Task = require('./models/task');
const Report = require('./models/report');

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
	socket.on('pythonConnectionRequest', function() {
		console.log('Learning System connected...');
		socket.join('learning-system');
	});
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
		supervisorConfiguration.active =
			supervisorConfiguration.active == true ? false : true;
		console.log(
			'Supervisor Client is requesting to toggle state!',
			supervisorConfiguration.active
		);
		socket.send({
			event: 'RES:toggleSupervisor',
			data: supervisorConfiguration
		});
	});

	socket.on('newTask', function(params) {
		var tempTask = new Task(params);
		tempTask.save(function(err, temp) {
			if (err) console.log('Error while creating new task template. ', err);
			var tempReport = new Report({ task: temp.id });
			tempReport.save(function(err, tempReport) {
				console.log('Creating new report...');
				if (err) throw err;
				Report.findById(tempReport.id, function(err, report) {
					if (err) throw err;
					console.log('Sending report...', report);
					socket.send({ event: 'RES:newReport', data: report });
				});
			});

			Task.findById(temp.id, function(err, task) {
				if (err)
					console.log(
						'Error while retrieving the newly created task template. ',
						err
					);
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

	socket.on('getReportByTaskID', function(task_id) {
		console.log('Client requesting for Task Report');
		Report.find({ task: mongoose.ObjectId(task_id) }, function(err, report) {
			socket.send({ event: 'RES:getReportByTaskID', data: report });
		});
	});

	socket.on('trainTaskByID', function(id) {
		console.log('Client requesting trainTaskByID on: ', id);
		io
			.to('learning-system')
			.emit('LS:trainRequest', { clientID: socket.id, taskID: id });
	});

	socket.on('LSRES:trainRequest', function(response) {
		switch (response.event) {
			case 'ACK': {
				io.to(response.clientID).emit('RES:trainRequest', {
					event: response.event,
					data: response.data,
					_id: response._id
				});
				break;
			}

			case 'UPDATE_TASK': {
				Task.findById(mongoose.Types.ObjectId(response._id), function(
					err,
					task
				) {
					if (err) throw err;

					io
						.to(response.clientID)
						.send({ event: 'RES:updateTask', data: task });
				});
				break;
			}

			case 'END_TRAINING': {
				console.log('Reaching here...');
				Report.find({ task: response._id }, function(err, report) {
					if (err) throw err;

					io
						.to(response.clientID)
						.send({ event: 'RES:newReport', data: report });
				});
				break;
			}
		}
	});
});
