import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

import 'rxjs/add/operator/map';

import { AppStore } from '../models/appstore.model';
import { QueryResult } from '../models/queryResult.model';

import * as io from 'socket.io-client';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class TestService {
  currentQueryResult$: Observable<QueryResult>;
  private socket: SocketIOClient.Socket;

  constructor(private store: Store<AppStore>) {
    this.currentQueryResult$ = store.select('queryResult');
    this.socket = io('http://localhost:8081');
    this.socket.on('RES:testQuery', function(response) {
      store.dispatch({
        type: 'SET_QUERY_RESULT',
        payload: response.data
      });
    });
  }

  submitQuery(taskID, query) {
    this.store.dispatch({
      type: 'RESET_QUERY_RESULT'
    });
    this.socket.emit('testQuery', { taskID: taskID, query: query });
  }
}
