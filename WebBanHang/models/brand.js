const mongoose = require('mongoose');

const Model = new mongoose.Schema(
  {
    id: Number,
    name:  String,
    isDeleted: Boolean
  },
  {
    collection: 'brand'
  }
);
    
Model.plugin(require('../modules/auto-increment').getInstance().plugin, {
  model: 'brand',
  field: 'id'
});

module.exports = mongoose.model('brand', Model);
