// Import task model, used for defining initial state
import { Task as State } from '../models/task.model';

// Import action declarations
import * as StoreActions from '../actions/store.actions';

export type Action = StoreActions.allTaskActions;

// Reducer definition
export function reducer(state: State[] = null, action: Action) {
	switch (action.type) {
		case StoreActions.ADD_TASK: {
			return state == null ? [action.payload] : [action.payload, ...state];
		}

		case StoreActions.UPDATE_TASK: {
			return state == null
				? [action.payload]
				: state.map(task => {
						return task._id === action.payload._id ? Object.assign({}, task, action.payload) : task;
					});
		}

		default: {
			return state;
		}
	}
}
