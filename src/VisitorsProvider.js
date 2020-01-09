import openSocket from 'socket.io-client';

export default class VisitorsProvider {
  unknownVisitorCallback;
  approvedVisitorCallback;

  // onUnknownVisitor(cb) {
  //   this.unknownVisitorCallback = cb;
  // }

  onApprovedVisitor(cb) {
    this.approvedVisitorCallback = cb;
  }

  start() {
    const socket = openSocket('http://localhost:5000');

    socket.on('connect', () => console.log('connected to the server!'));

    // socket.on('newUnknownVisitor', data => this.approvedVisitorCallback(data));
    socket.on('newApprovedVisitor', data => this.approvedVisitorCallback(data));

    socket.on('disconnect', () => console.log('disconnect'));
  }
}
