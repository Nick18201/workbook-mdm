from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_business_plan(output_filename="Workbook_Business_Plan.pdf"):
    """Le livret « Mon business plan », compiled from workbooks/business_plan.json."""
    build_reference_workbook("business_plan", output_filename)


build_workbook_business_plan = generate_workbook_business_plan


if __name__ == "__main__":
    args = create_cli(description="Générer le livret interactif 'Mon Business Plan' (PDF).", default_output="Workbook_Business_Plan.pdf")
    generate_workbook_business_plan(args.output)
