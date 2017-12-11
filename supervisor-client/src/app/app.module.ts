import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { ClarityModule } from 'clarity-angular';
import { ChartsModule } from 'ng2-charts';

import { AppComponent } from './app.component';
// import { BarChartDemoComponent } from './app.component';
// import {SkewComponent} from './app.component';
import { HeaderComponent } from './header/header.component';
import { ClientComponent } from './client/client.component';
import { SupervisorComponent } from './supervisor/supervisor.component';
import { ReportComponent } from './report/report.component';

// ngrx main imports
import { StoreModule } from '@ngrx/store';

// service imports
import { DatasetService } from './store/services/dataset.service';
import { SupervisorService } from './store/services/supervisor.service';
import { TaskService } from './store/services/task.service';

// reducer imports
import { reducer as datasetReducer } from './store/reducers/dataset.reducer';
import { reducer as supervisorReducer } from './store/reducers/supervisor.reducer';
import { reducer as taskReducer } from './store/reducers/task.reducer';
import { reducer as reportReducer } from './store/reducers/report.reducer';
import { IdFilterPipe } from './id-filter.pipe';
import { NgPipesModule } from 'ngx-pipes';

const appRoutes: Routes = [
  { path: 'client', component: ClientComponent },
  { path: 'supervisor', component: SupervisorComponent },
  { path: 'report/:id', component: ReportComponent },
  {
    path: '',
    redirectTo: 'client',
    pathMatch: 'full'
  }
  // { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ClientComponent,
    SupervisorComponent,
    ReportComponent,
    IdFilterPipe
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    ChartsModule,
    NgPipesModule,
    RouterModule.forRoot(appRoutes, { enableTracing: true }),
    ClarityModule.forRoot(),
    StoreModule.forRoot({
      availableDatasets: datasetReducer,
      supervisorConfiguration: supervisorReducer,
      currentTasks: taskReducer,
      currentReports: reportReducer
    })
  ],
  providers: [DatasetService, SupervisorService, TaskService],
  bootstrap: [AppComponent]
})
export class AppModule {}
