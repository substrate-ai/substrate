// create a ecr repository



resource "aws_ecr_repository" "ecr" {
    image_tag_mutability = "MUTABLE"
    image_scanning_configuration {
        scan_on_push = true
    }
}

