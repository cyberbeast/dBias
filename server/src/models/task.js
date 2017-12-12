const mongoose = require('mongoose');
var Schema = mongoose.Schema;

var taskSchema = new Schema({
	name: {
		type: String,
		default: ''
	},
	description: {
		type: String,
		default: ''
	},
	dataset: {
		type: String,
		default: ''
	},
	type: {
		type: String,
		default: ''
	},
	trained: {
		type: Boolean,
		default: false
	},
	best_training_accuracy: {
		type: Number,
		default: 0
	},
	best_training_model: {
		type: String,
		default: ''
	},
	action: {
		type: Boolean,
		default: false
	},
	supervisor: {
		type: Boolean,
		default: true
	}
});

var Task = mongoose.model('Task', taskSchema);

module.exports = Task;
