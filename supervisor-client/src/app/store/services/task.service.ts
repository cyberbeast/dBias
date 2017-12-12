import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

import 'rxjs/add/operator/map';

import { AppStore } from '../models/appstore.model';
import { Task } from '../models/task.model';
import { Report } from '../models/report.model';
import { Status } from '../models/status.model';

import * as io from 'socket.io-client';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class TaskService {
  currentTasks$: Observable<Task[]>;
  selectedTask$: Observable<Task>;
  selectedReport$: Observable<Report>;
  statusStream$ = new BehaviorSubject('');
  private socket: SocketIOClient.Socket;
  self = this;

  constructor(private store: Store<AppStore>) {
    this.currentTasks$ = store.select('currentTasks');
    this.selectedReport$ = store.select('selectedReport');
    this.selectedTask$ = store.select('selectedTask');
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

        case 'RES:newReport': {
          console.log('RES:newReport', response);
          store.dispatch({
            type: 'CREATE_REPORT',
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

        case 'RES:getTaskByID': {
          console.log('RES:getTaskByID', response);
          store.dispatch({
            type: 'SELECT_TASK',
            payload: response.data
          });
          break;
        }

        case 'RES:updateTask': {
          console.log('RES:updateTasks', response);
          store.dispatch({
            type: 'UPDATE_TASK',
            payload: response.data
          });
          break;
        }

        case 'RES:getReportByTaskID': {
          console.log('RES:getReportByTaskID', response);
          var sv_viz = [];
          var sv_distribution_by_salary = [];
          var u_viz = [];
          var model_details = [];
          response.data.analysis.map(a => {
            if (a.type === 'sv_report') {
              var toggle = true;
              var skewedToggle = true;

              a.content.map(val => {
                if (val.type == 'visualizations') {
                  if (val.data.name === 'DistributionBySalary') {
                    var temp = val.data;
                    temp['active'] = toggle == true ? true : false;
                    toggle = false;
                    sv_distribution_by_salary.push(temp);
                  } else if (val.data.name === 'Skewed Data') {
                    var temp = val.data;
                    temp['active'] = skewedToggle == true ? true : false;
                    skewedToggle = false;
                    sv_viz.push(val.data);
                  }
                } else if (val.type == 'model_details') {
                  model_details.push(val.data);
                }
              });
            }
          });
          console.log('RES:getReportByTaskID ', model_details);
          store.dispatch({
            type: 'SET_REPORT',
            payload: {
              _id: response.data._id,
              model_details: model_details,
              sv_visualizations: sv_viz,
              sv_distribution_by_salary: sv_distribution_by_salary,
              u_visualizations: u_viz
            }
          });
          break;
        }
      }
    });
  }

  selectTask(id) {
    this.socket.emit('getTaskByID', id);
  }

  selectReport(id) {
    this.socket.emit('getReportByTaskID', id);
  }

  getSystemTasks() {
    this.socket.emit('getTasks');
  }

  newTaskRequest(params) {
    this.socket.emit('newTask', params);
  }

  setNextMessageOnStatusStream(data) {
    this.statusStream$.next(data);
  }

  handler(response) {
    console.log('LS said: ', response);
    this.setNextMessageOnStatusStream({
      _id: response._id,
      message: response.data
    });
  }

  trainTaskByID(id) {
    this.socket.emit('trainTaskByID', id);
    this.socket.on('RES:trainRequest', this.handler.bind(this));
  }
}
