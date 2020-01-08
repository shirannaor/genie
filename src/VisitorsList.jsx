import 'react-table-v6/react-table.css';
import './VisitorsList.css';
import { FaCheckCircle } from 'react-icons/fa';

import ReactTable from 'react-table-v6';
import React from 'react';
import moment from 'moment';

import VisitorsProvider from './VisitorsProvider';

const DATA = [
  {
    name: 'Or Hamalka',
    startTime: new Date(Date.now() - 10 * 60 * 1000),
    endTime: new Date(Date.now() - 11 * 60 * 1000),
    approved: true
  },
  {
    name: 'Shiran Naor',
    startTime: new Date(Date.now() - 12 * 60 * 1000),
    endTime: new Date(Date.now() - 13 * 60 * 1000),
    approved: true
  }
];

const COLUMNS = [
  { Header: 'Name', accessor: 'name' },
  {
    Header: 'Start Time',
    accessor: 'startTime',
    Cell: props => (
      <span className="number">
        {moment(props.value).format('DD/MM/YY H:mm:ss')}
      </span>
    )
  },
  {
    Header: 'End Time',
    accessor: 'endTime',
    Cell: props => (
      <span className="number">
        {moment(props.value).format('DD/MM/YY H:mm:ss')}
      </span>
    )
  },
  {
    Header: 'Approved',
    accessor: 'approved',
    Cell: props => (props.value ? <FaCheckCircle /> : 'No')
  }
];

export default class VisitorsList extends React.Component {
  state = {
    visitors: DATA
  };

  componentDidMount() {
    const provider = new VisitorsProvider();
    provider.onUnknownVisitor(this._onUnknownVisitor);
    provider.onApprovedVisitor(this._onApprovedVisitor);

    provider.start();
  }

  render() {
    return (
      <ReactTable
        className="visitors-list"
        data={this.state.visitors}
        columns={COLUMNS}
        defaultPageSize={10}
      />
    );
  }

  _onUnknownVisitor() {
    // TODO
  }

  _onApprovedVisitor() {
    // TODO
  }
}
