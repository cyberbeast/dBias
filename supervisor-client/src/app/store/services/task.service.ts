import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

import 'rxjs/add/operator/map';

import { AppStore } from '../models/appstore.model';
import { Task } from '../models/task.model';

import * as io from 'socket.io-client';

@Injectable()
export class TaskService {
  currentTasks$: Observable<Task[]>;

  private socket: SocketIOClient.Socket;

  constructor(private store: Store<AppStore>) {
    this.currentTasks$ = store.select('currentTasks');
    this.socket = io('http://localhost:8081');
    this.socket.on('message', function(response) {
      switch (response.event) {
        case 'RES:newTask': {
          console.log('RES:newTask', response);
          store.dispatch({
            type: 'ADD_TASK',
            payload: response.data
          });
          break;
        }

        case 'RES:getTasks': {
          console.log('RES:getTasks', response);
          store.dispatch({
            type: 'CREATE_TASK',
            payload: response.data
          });
          break;
        }
      }
    });
  }

  getSystemTasks() {
    this.socket.emit('getTasks');
  }

  newTaskRequest(params) {
    this.socket.emit('newTask', params);
  }

  trainTaskByID(id) {
    this.socket.emit('trainTaskByID', id);
    this.socket.on('RES:trainRequest', function(response) {
      console.log('LS said: ', response);
    });
  }
}
