// Import supervisor model, used for defining initial state
import { Supervisor as State } from '../models/supervisor.model';

// Import action declarations
import * as StoreActions from '../actions/store.actions';

export type Action = StoreActions.allSupervisorActions;

// Define initial state
const initialState: State = {
	active: false
};

// Reducer definition
export function reducer(state: State = initialState, action: Action) {
	switch (action.type) {
		case StoreActions.TOGGLE_SUPERVISOR: {
			return Object.assign({}, state, { active: state.active == true ? false : true });
		}

		case StoreActions.GET_SUPERVISOR: {
			return action.payload;
		}

		default: {
			return state;
		}
	}
}
