import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';

import 'rxjs/add/operator/map';

import { AppStore } from '../models/appstore.model';
import { Dataset } from '../models/dataset.model';

import * as io from 'socket.io-client';

@Injectable()
export class DatasetService {
	availableDatasets$: Observable<Dataset[]>;
	private socket: SocketIOClient.Socket;

	constructor(private store: Store<AppStore>) {
		this.availableDatasets$ = store.select('availableDatasets');
		this.socket = io('http://localhost:8081');
		this.socket.on('message', function(response) {
			switch (response.event) {
				case 'RES:getDatasets': {
					console.log('Server said...', response);
					store.dispatch({
						type: 'GET_DATASETS',
						payload: response.data
					});
					break;
				}
			}
		});
	}

	refreshDatasets() {
		this.socket.emit('getDatasets');
	}

	activateDataset(datasetName: string) {
		this.store.dispatch({
			type: 'SET_DATASET',
			payload: datasetName
		});
	}
}
