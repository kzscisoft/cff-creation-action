library(desc)
library(yaml)
args = commandArgs(trailingOnly=TRUE)
desc <- description$new(args[1])
authors_list <- c()

for(i in 1:length(desc$get_authors()))
{
    name <- desc$get_authors()[i]
    author <- list(`family-names`=name$family, `given-names`=name$given)
    authors_list[[i]] <- author
}

cff_output <- list(
    version = desc$get("Version"),
    title = desc$get("Title"),
    license = desc$get("License")
)

if(length(authors_list) > 0)
{
    cff_output$authors = authors_list
}

if(!is.na(desc$get("URL")))
{
    cff_output$url = desc$get("URL")
}

write_yaml(cff_output, 'CITATION.cff')