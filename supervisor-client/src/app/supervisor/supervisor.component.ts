import { Component, OnInit } from '@angular/core';
import { SupervisorService } from '../store/services/supervisor.service';
import { Supervisor } from '../store/models/supervisor.model';

@Component({
	selector: 'app-supervisor',
	templateUrl: './supervisor.component.html',
	styleUrls: ['./supervisor.component.css']
})
export class SupervisorComponent implements OnInit {
	supervisorConfiguration: Supervisor;

	constructor(private _supervisorService: SupervisorService) {}

	getInitServerState() {
		this._supervisorService.collectSupervisorConfiguration();
	}

	toggle() {
		this._supervisorService.toggleSupervisor();
	}

	ngOnInit() {
		this.getInitServerState();
		this._supervisorService.currentSupervisorConfiguration$.subscribe(config => {
			this.supervisorConfiguration = config;
		});
	}
}
