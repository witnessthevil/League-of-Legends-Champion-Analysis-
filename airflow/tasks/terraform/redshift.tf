resource "aws_redshift_cluster" "example" {
  cluster_identifier = "tf-daniel-clustering"
  database_name      = "lol_stat2"
  master_username    = var.redshift-admin-user
  master_password    = var.redshift-admin-master_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  publicly_accessible   = true
  vpc_security_group_ids = [aws_security_group.redshift_security_group_2.id]
}

resource "aws_security_group" "redshift_security_group_2" {
  name = "redshift_security_group_lol"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}