import { Action } from '@ngrx/store';
import { Dataset } from '../models/dataset.model';
import { Supervisor } from '../models/supervisor.model';
import { Task } from '../models/task.model';
import { Report } from '../models/report.model';
import { QueryResult } from '../models/queryResult.model';

// Actions for Dataset model.
export const SET_DATASET: string = 'SET_DATASET';
export const GET_DATASETS: string = 'GET_DATASETS';

export class SetDataset implements Action {
  readonly type = SET_DATASET;
  constructor(public payload: Dataset) {}
}

export class GetDatasets implements Action {
  readonly type = GET_DATASETS;
  constructor(public payload: any) {}
}

export type allDatasetActions = SetDataset | GetDatasets;

// Actions for Supervisor model.
export const TOGGLE_SUPERVISOR: string = 'TOGGLE_SUPERVISOR';
export const GET_SUPERVISOR: string = 'GET_SUPERVISOR';

export class ToggleSupervisor implements Action {
  readonly type = TOGGLE_SUPERVISOR;
  constructor(public payload: null) {}
}

export class GetSupervisor implements Action {
  readonly type = GET_SUPERVISOR;
  constructor(public payload: Supervisor) {}
}

export type allSupervisorActions = ToggleSupervisor | GetSupervisor;

// Actions for Task model.
export const ADD_TASK: string = 'ADD_TASK';
export const UPDATE_TASK: string = 'UPDATE_TASK';
export const CREATE_TASK: string = 'CREATE_TASK';

export class AddTask implements Action {
  readonly type = ADD_TASK;
  constructor(public payload: Task) {}
}

export class UpdateTask implements Action {
  readonly type = UPDATE_TASK;
  constructor(public payload: Task) {}
}

export class CreateTask implements Action {
  readonly type = CREATE_TASK;
  constructor(public payload: Task) {}
}
export type allTaskActions = AddTask | UpdateTask | CreateTask;

export const SELECT_TASK: string = 'SELECT_TASK';
export class SelectTask implements Action {
  readonly type = SELECT_TASK;
  constructor(public payload: Task) {}
}
export type allSelectTaskActions = SelectTask;

// Actions for Report Model.
export const SET_REPORT: string = 'SET_REPORT';

export class SetReport implements Action {
  readonly type = SET_REPORT;
  constructor(public payload: Report) {}
}

export type allReportActions = SetReport;

// Actions for queryResult Model.
export const SET_QUERY_RESULT: string = 'SET_QUERY_RESULT';
export const RESET_QUERY_RESULT: string = 'RESET_QUERY_RESULT';

export class SetQueryResult implements Action {
  readonly type = SET_QUERY_RESULT;
  constructor(public payload: QueryResult) {}
}

export class ResetQueryResult implements Action {
  readonly type = RESET_QUERY_RESULT;
  constructor(public payload: QueryResult) {}
}

export type allQueryResultActions = SetQueryResult | ResetQueryResult;
