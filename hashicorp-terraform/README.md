# Terraform 

Terraform is a IaC (Infrastructure as a Code) tool that helps to accelerate infrastructure provisioning on Cloud providers, helping tem manage its infrstructure as a code in a repetable and reproduceble way.

## Other common Infrastucture as a Code tools

- terraform
- ansible
- puppet
- packer
- vagrant
- docker
- puppet

Although they are all infrastructure as a code tools, all theses tools will always fall into three categories:

 - Configuration Management: ansible, puppet, salt stack, chef
 - Server Templating: docker, vagrant, packer
 - Provisiosioning tools: cloudformation, terraform


## HCL - Hashicorp Language

The HCL is declarative language, it means that the desired state of a given configuration must be written in the terraform template.

There is always three phases when we work with terraform templates

1. init (initialization phase)
2. plan (terraform plans the logig to apply the desired configurationwriteen in the template)
3. apply (terraform applies the configuration)

## HCL - The syntax

<block> <parameters>{
    key1 = value1
}

## Terraform Registry

The terraform registry is the place where we can get all the terraform providers source code and also its documentation. We can take a look on that by accessing the website:

- https://registry.terraform.io/

The terraform providers fall under these categories:

1. Official (AWS, Azure, GCP, Terraform, Alibaba)
2. Partner (Turbot, F5, Heroku and etc)

When we use the terraform init command it checks the provider declared on the template and then performs the download for all the provider dependencies.

These dependency are called plugins

## The terraform structure directory


## Terraform Variables
 We can set variables values by passing some inputs by exporting some operating system varibales TF_VAR_name_of_the_variable.

 Precednece order

 4. OS variables
 3. terrafor.tfvars
 2. *.auto.tfvars (alphabetical order)
 1. Command Line  terraform apply -var {pass the variable name and values}

 The precendece order is very important


## Dependency

Explcity
Implicity
 ## Outputs

 ## Interpolation

