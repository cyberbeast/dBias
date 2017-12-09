import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';

import 'rxjs/add/operator/map';

import { AppStore } from '../models/appstore.model';
import { Dataset } from '../models/dataset.model';

@Injectable()
export class DatasetService {
	availableDatasets$: Observable<Dataset[]>;

	constructor(private store: Store<AppStore>) {
		this.availableDatasets$ = store.select('availableDatasets');
	}

	refreshDatasets() {
		// console.log('users(SERVICE) : Invoked updatePreferences method -> ' + JSON.stringify(newPreferences));
		// this.store.dispatch({
		// 	type: 'UPDATE_PREFERENCES',
		// 	payload: newPreferences
		// });
	}

	activateDataset(datasetName: string) {
		this.store.dispatch({
			type: 'SET_DATASET',
			payload: datasetName
		});
	}
}
