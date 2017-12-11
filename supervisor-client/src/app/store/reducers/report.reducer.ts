// Import task model, used for defining initial state
import { Report as State } from '../models/report.model';

// Import action declarations
import * as StoreActions from '../actions/store.actions';

export type Action = StoreActions.allReportActions;

// Reducer definition
export function reducer(state: State[] = null, action: Action) {
  switch (action.type) {
    case StoreActions.UPDATE_REPORT: {
      return state.map(report => {
        return report._id === action.payload._id
          ? Object.assign({}, report, action.payload)
          : report;
      });
    }

    case StoreActions.CREATE_REPORT: {
      return action.payload;
    }

    default: {
      return state;
    }
  }
}
