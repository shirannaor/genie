import 'react-table-v6/react-table.css';
import './VisitorsList.css';
import { FaCheckCircle, FaMinusCircle } from 'react-icons/fa';

import ReactTable from 'react-table-v6';
import React from 'react';
import moment from 'moment';

import VisitorsProvider from './VisitorsProvider';

const COLUMNS = [
  { Header: 'Name', accessor: 'name' },
  {
    Header: 'When',
    accessor: 'time',
    Cell: props => <span>{moment(props.value).format('DD/MM/YY H:mm:ss')}</span>
  },
  {
    Header: 'Approved',
    accessor: 'approved',
    Cell: props => (props.value ? <FaCheckCircle /> : <FaMinusCircle />)
  }
];

export default class VisitorsList extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      visitors: []
    };
  }

  componentDidMount() {
    const provider = new VisitorsProvider();
    // provider.onUnknownVisitor(this._onUnknownVisitor);
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

  _onApprovedVisitor = name => {
    const visitors = [
      ...this.state.visitors,
      { name, time: Date.now(), approved: name !== 'Unknown' }
    ];

    this.setState({ visitors });
  };
}
