#!/usr/bin/env python3
"""Calculate comparable ROI scenarios for audit automation projects."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from typing import Iterable


@dataclass
class ModelPrice:
    name: str
    input_million: float
    cached_input_million: float
    output_million: float


def model_cost_cny(
    orders_per_month: float,
    input_tokens: float,
    output_tokens: float,
    fixed_input_tokens: float,
    price: ModelPrice,
    usd_cny: float,
    call_ratio: float = 1.0,
) -> tuple[float, float]:
    """Return annual cost range: cached-fixed lower bound, all-cache-miss upper bound."""
    variable_input = max(input_tokens - fixed_input_tokens, 0.0)
    lower_usd_per_order = (
        fixed_input_tokens * price.cached_input_million
        + variable_input * price.input_million
        + output_tokens * price.output_million
    ) / 1_000_000
    upper_usd_per_order = (
        input_tokens * price.input_million
        + output_tokens * price.output_million
    ) / 1_000_000
    multiplier = orders_per_month * 12 * call_ratio * usd_cny
    return lower_usd_per_order * multiplier, upper_usd_per_order * multiplier


def fmt_range(values: tuple[float, float]) -> str:
    return f"{values[0]:,.0f}～{values[1]:,.0f}"


def pct_range(savings: tuple[float, float], baseline: float) -> str:
    return f"{savings[0] / baseline * 100:.1f}%～{savings[1] / baseline * 100:.1f}%"


def build_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    domestic = ModelPrice(
        "domestic",
        args.domestic_input,
        args.domestic_cached_input,
        args.domestic_output,
    )
    overseas = ModelPrice(
        "overseas",
        args.overseas_input,
        args.overseas_cached_input,
        args.overseas_output,
    )

    manual_personnel = args.doctor_annual_cost * args.doctor_audit_ratio + (
        args.operator_annual_cost * args.operator_audit_ratio
    )
    operator_cost = args.operator_annual_cost * args.operator_audit_ratio

    def personnel(review_ratio: float, scale_operator: bool) -> float:
        doctor = args.doctor_annual_cost * args.doctor_audit_ratio * review_ratio
        op = operator_cost * (review_ratio / args.current_review_ratio) if scale_operator else operator_cost
        return doctor + op

    def row(name: str, personnel_cost: float, model_cost: tuple[float, float]) -> dict[str, str]:
        total = (personnel_cost + model_cost[0], personnel_cost + model_cost[1])
        savings = (manual_personnel - total[1], manual_personnel - total[0])
        return {
            "scenario": name,
            "personnel_cost_cny_year": f"{personnel_cost:,.2f}",
            "model_cost_cny_year": fmt_range(model_cost),
            "total_cost_cny_year": fmt_range(total),
            "savings_vs_manual_cny_year": fmt_range(savings),
            "savings_rate_vs_manual": pct_range(savings, manual_personnel),
        }

    full_domestic = model_cost_cny(
        args.orders_per_month,
        args.input_tokens,
        args.output_tokens,
        args.fixed_input_tokens,
        domestic,
        args.usd_cny,
    )
    full_overseas = model_cost_cny(
        args.orders_per_month,
        args.input_tokens,
        args.output_tokens,
        args.fixed_input_tokens,
        overseas,
        args.usd_cny,
    )

    current_people = personnel(args.current_review_ratio, scale_operator=False)
    long_people_fixed = personnel(args.long_run_review_ratio, scale_operator=False)
    long_people_scaled = personnel(args.long_run_review_ratio, scale_operator=True)

    overseas_current_exception = model_cost_cny(
        args.orders_per_month,
        args.input_tokens,
        args.output_tokens,
        args.fixed_input_tokens,
        overseas,
        args.usd_cny,
        call_ratio=args.current_review_ratio,
    )
    overseas_long_exception = model_cost_cny(
        args.orders_per_month,
        args.input_tokens,
        args.output_tokens,
        args.fixed_input_tokens,
        overseas,
        args.usd_cny,
        call_ratio=args.long_run_review_ratio,
    )

    hybrid_current = (
        full_domestic[0] + overseas_current_exception[0],
        full_domestic[1] + overseas_current_exception[1],
    )
    hybrid_long = (
        full_domestic[0] + overseas_long_exception[0],
        full_domestic[1] + overseas_long_exception[1],
    )

    zero = (0.0, 0.0)
    return [
        row("pure_manual_baseline", manual_personnel, zero),
        row("domestic_current_review", current_people, full_domestic),
        row("overseas_current_review", current_people, full_overseas),
        row("hybrid_current_review", current_people, hybrid_current),
        row("domestic_long_run_fixed_operator", long_people_fixed, full_domestic),
        row("domestic_long_run_scaled_operator", long_people_scaled, full_domestic),
        row("hybrid_long_run_fixed_operator", long_people_fixed, hybrid_long),
        row("hybrid_long_run_scaled_operator", long_people_scaled, hybrid_long),
    ]


def write_csv(rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
    writer = csv.DictWriter(__import__("sys").stdout, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orders-per-month", type=float, required=True)
    parser.add_argument("--input-tokens", type=float, default=3500)
    parser.add_argument("--output-tokens", type=float, default=1000)
    parser.add_argument("--fixed-input-tokens", type=float, default=2000)
    parser.add_argument("--usd-cny", type=float, default=6.7935)
    parser.add_argument("--doctor-annual-cost", type=float, required=True)
    parser.add_argument("--doctor-audit-ratio", type=float, required=True)
    parser.add_argument("--operator-annual-cost", type=float, required=True)
    parser.add_argument("--operator-audit-ratio", type=float, required=True)
    parser.add_argument("--current-review-ratio", type=float, default=0.15)
    parser.add_argument("--long-run-review-ratio", type=float, default=0.03)
    parser.add_argument("--domestic-input", type=float, required=True)
    parser.add_argument("--domestic-cached-input", type=float, required=True)
    parser.add_argument("--domestic-output", type=float, required=True)
    parser.add_argument("--overseas-input", type=float, required=True)
    parser.add_argument("--overseas-cached-input", type=float, required=True)
    parser.add_argument("--overseas-output", type=float, required=True)
    write_csv(build_rows(parser.parse_args()))


if __name__ == "__main__":
    main()
