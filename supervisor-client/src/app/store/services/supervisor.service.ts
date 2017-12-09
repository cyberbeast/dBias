import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';

import 'rxjs/add/operator/map';

import { AppStore } from '../models/appstore.model';
import { Supervisor } from '../models/supervisor.model';

import * as io from 'socket.io-client';

@Injectable()
export class SupervisorService {
	currentSupervisorConfiguration$: Observable<Supervisor>;
	private socket: SocketIOClient.Socket;

	constructor(private store: Store<AppStore>) {
		this.currentSupervisorConfiguration$ = store.select('supervisorConfiguration');
		this.socket = io('http://localhost:8081');
		this.socket.on('message', function(response) {
			switch (response.event) {
				case 'RES:getSupervisorConfiguration': {
					console.log('Server said...', response);
					store.dispatch({
						type: 'GET_SUPERVISOR',
						payload: response.data
					});
					break;
				}
				case 'RES:toggleSupervisor': {
					console.log('Server said...', response.data.active);
					store.dispatch({
						type: 'GET_SUPERVISOR',
						payload: response.data
					});
					break;
				}
			}
		});
	}

	collectSupervisorConfiguration() {
		this.socket.emit('getSupervisorConfiguration');
	}

	toggleSupervisor() {
		this.store.dispatch({
			type: 'TOGGLE_SUPERVISOR',
			payload: null
		});
		this.socket.emit('toggleSupervisor');
	}
}
