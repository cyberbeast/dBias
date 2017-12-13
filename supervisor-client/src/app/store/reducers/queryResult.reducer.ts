// Import queryResult model, used for defining initial state
import { QueryResult as State } from '../models/queryResult.model';

// Import action declarations
import * as StoreActions from '../actions/store.actions';

export type Action = StoreActions.allQueryResultActions;

// Define initial state
const initialState: State = {
  columns: [''],
  index: [0],
  data: [{}],
  resultCount: 0
};

// Reducer definition
export function reducer(state: State = initialState, action: Action) {
  switch (action.type) {
    case StoreActions.SET_QUERY_RESULT: {
      return action.payload;
    }

    case StoreActions.RESET_QUERY_RESULT: {
      return initialState;
    }

    default: {
      return state;
    }
  }
}
