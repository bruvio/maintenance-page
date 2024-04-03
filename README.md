# HTO maintenance page

This repo deployes a maintenance page.

The logic is simple.

Collects all the hosts listed under a listener.
Deprioritize the current rules (adding +100)
creates news rule for each host that redirect to the maintenance page

to tear down the page the logic is inverted:

removes the newly created rules with redirection to the maintenance page
swift down the priorities of the original rules.


Prerequisite is to collect the hosts for all enviroments.
This is done using the python script `aws_alb_host.py`

At the time of creating this repo the host for each enviroment are populated in the tfvars.

The Jupyter notebook `alb.ipynb` allows to backup the current listener rules and in case of errors can restore from a json file.
So before making any changes to the logic is preferable to run a backup first.

## Deployment
to deploy the maintenance page (in dev)
```TF_VAR_maintenance_mode=true  terraform apply -var-file=dev.tfvars```
to tear down the maintenance page and restore traffic (in dev)

```TF_VAR_maintenance_mode=false  terraform apply -var-file=dev.tfvars```



