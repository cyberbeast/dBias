const mongoose = require('mongoose');
var Schema = mongoose.Schema;

var reportSchema = new Schema({
	task: Schema.ObjectId,
	sv_report: {
		type: Object,
		default: {}
	},
	u_report: {
		type: Object,
		default: {}
	}
});

var Report = mongoose.model('Report', reportSchema);

module.exports = Report;
