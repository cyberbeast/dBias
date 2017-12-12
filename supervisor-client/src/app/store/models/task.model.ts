export interface Task {
  _id: string;
  name: string;
  description: string;
  dataset: string;
  type: string;
  trained: boolean;
  best_training_accuracy: number;
  best_training_model: string;
  action: boolean;
  supervisor: boolean;
}
