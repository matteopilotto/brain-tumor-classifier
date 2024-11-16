provider "aws" {
    profile = "default"
    region = "us-east-1"
}

resource "aws_vpc" "brain_cls_vpc" {
    cidr_block = "10.0.0.0/24"

    tags = {
        Name = "brain_cls_vpc"
    }
}

resource "aws_subnet" "brain_cls_subnet" {
    vpc_id = aws_vpc.brain_cls_vpc.id
    cidr_block = "10.0.0.0/24"
    availability_zone = "us-east-1a"

    tags = {
        Name = "brain_cls_subnet"
    }
}

resource "aws_internet_gateway" "brain_cls_igw" {
    vpc_id = aws_vpc.brain_cls_vpc.id

    tags = {
        Name = "brain_cls_igw"
    }
}

resource "aws_route_table" "brain_cls_rt" {
    vpc_id = aws_vpc.brain_cls_vpc.id
    
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.brain_cls_igw.id
    }

    tags = {
        Name = "brain_csl_rt"
    }
}

resource "aws_route_table_association" "brain_cls_rta" {
    subnet_id = aws_subnet.brain_cls_subnet.id
    route_table_id = aws_route_table.brain_cls_rt.id
}

resource "aws_security_group" "brain_cls_sg" {
    name = "brain_cls_sg"
    vpc_id = aws_vpc.brain_cls_vpc.id

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 8501
        to_port = 8501
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "brain_cls_instance" {
    ami = "ami-063d43db0594b521b"
    instance_type = "t3.large"
    key_name = "brain_cls"
    vpc_security_group_ids = [aws_security_group.brain_cls_sg.id]
    subnet_id = aws_subnet.brain_cls_subnet.id
    associate_public_ip_address = true

    root_block_device {
        volume_size = 20
        volume_type = "gp3"
        delete_on_termination = true
    }

    user_data = <<-EOF
                #!/bin/bash
                sudo yum update -y
                # sudo yum install git -y
                EOF

    tags = {
        Name = "brain_cls_instance"
    }
}