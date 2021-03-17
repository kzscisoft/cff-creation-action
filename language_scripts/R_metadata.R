#!/usr/bin/R
library(desc)
library(yaml)
library(optparse)

DEFAULT_MSG <- "If you use this software, please cite it using these metadata."

option_list <- list(
    make_option(c("-i", "--input-file"), type="character", default="DESCRIPTION", metavar="character"),
    make_option(c("-m", "--message"), type="character", default=DEFAULT_MSG, metavar="character"),
    make_option(c("-v", "--cff-version"), type="character", default="1.1.0", metavar="character"),
    make_option(c("-a", "--affiliation", type="character", default=NA, metavar="character"))
)

parser <- OptionParser(option_list=option_list)
opt <- parse_args(parser)

desc <- description$new(opt$`input-file`)
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
    license = desc$get("License"),
    `cff-version` = opt$`cff-version`,
    message = opt$message
)

if(length(authors_list) > 0)
{
    if(length(opt$affiliation) > 0)
    {
        for(i in 1:length(authors_list))
        {
            authors_list[[i]]$affiliation = opt$affiliation
        }
    }
    cff_output$authors = authors_list
}

if(!is.na(desc$get("URL")))
{
    cff_output$url = desc$get("URL")
}

write_yaml(cff_output, 'CITATION.cff')