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
	accuracy: {
		type: Number,
		default: 0
	},
	action: {
		type: Boolean,
		default: false
	}
});

var Task = mongoose.model('Task', taskSchema);

module.exports = Task;
