import { Action } from '@ngrx/store';
import { Dataset } from '../models/dataset.model';
import { Supervisor } from '../models/supervisor.model';

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
