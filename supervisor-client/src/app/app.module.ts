import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClarityModule } from 'clarity-angular';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { ClientComponent } from './client/client.component';
import { SupervisorComponent } from './supervisor/supervisor.component';

// ngrx main imports
import { StoreModule } from '@ngrx/store';

// service imports
import { DatasetService } from './store/services/dataset.service';
import { SupervisorService } from './store/services/supervisor.service';

// reducer imports
import { reducer as datasetReducer } from './store/reducers/dataset.reducer';
import { reducer as supervisorReducer } from './store/reducers/supervisor.reducer';

const appRoutes: Routes = [
	{ path: 'client', component: ClientComponent },
	{ path: 'supervisor', component: SupervisorComponent },
	{
		path: '',
		redirectTo: 'client',
		pathMatch: 'full'
	}
	// { path: '**', component: PageNotFoundComponent }
];

@NgModule({
	declarations: [AppComponent, HeaderComponent, ClientComponent, SupervisorComponent],
	imports: [
		BrowserModule,
		RouterModule.forRoot(appRoutes, { enableTracing: true }),
		ClarityModule.forRoot(),
		StoreModule.forRoot({
			availableDatasets: datasetReducer,
			supervisorConfiguration: supervisorReducer
		})
	],
	providers: [DatasetService, SupervisorService],
	bootstrap: [AppComponent]
})
export class AppModule {}
