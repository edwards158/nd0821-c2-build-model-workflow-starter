#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    logger.info("Basic cleaning")
    # Drop outliers
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Write cleaned data")
    df.to_csv(args.output_artifact)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )

    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)

    artifact.wait()
    logger.info("Cleaned dataset uploaded to wandb")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="basic data cleaning")

    parser.add_argument(
        "--tmp_directory",
        type=str,
        help="Temporary directory for dataset storage",
        required=True
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully qualifed name for input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Fully qualifed name for output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Type for the artifact",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description for the artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="input value",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="input value",
        required=True
    )

    args = parser.parse_args()

    go(args)