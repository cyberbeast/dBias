import { Action } from '@ngrx/store';
import { Dataset } from '../models/dataset.model';

// Actions for mode model.
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
