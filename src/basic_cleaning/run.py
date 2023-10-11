#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    logger.info("Downloading and reading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path, low_memory=False)

    ######################
    # YOUR CODE HERE     #
    ######################
    df['last_review'] = pd.to_datetime(df['last_review'])
    df = df['price'].between(args.min_price, args.max_price)
    df.to_csv("clean_sample.csv", index=False)

    logger.info("Create new artifact")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)
    run.finish()
    os.remove(args.output_artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name of input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name of output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Type of output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Mininum acceptable rental price",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum acceptable rental price",
        required=True
    )

    args = parser.parse_args()

    go(args)
