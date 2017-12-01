#! node

const ansible = require('ansible-node-module');

ansible.main(() => {
    // TO DO
    return {
      change: false,
      msg: "hi!"
    };
});
