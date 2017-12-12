const mongoose = require('mongoose');
var Schema = mongoose.Schema;

var reportSchema = new Schema({
	task: Schema.ObjectId,
	analysis: {
		type: Array,
		default: []
	}
});

var Report = mongoose.model('Report', reportSchema);

module.exports = Report;
