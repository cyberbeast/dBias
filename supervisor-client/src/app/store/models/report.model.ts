export interface Report {
  _id: string;
  model_details: object[];
  sv_visualizations: object[];
  sv_distribution_by_salary: object[];
  u_visualizations?: object[];
}
