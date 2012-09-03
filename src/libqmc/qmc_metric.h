/*
 * Copyright (c) 2012 Red Hat.
 * Copyright (c) 2007 Aconex.  All Rights Reserved.
 * Copyright (c) 1998-2005 Silicon Graphics, Inc.  All Rights Reserved.
 * 
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published
 * by the Free Software Foundation; either version 2.1 of the License, or
 * (at your option) any later version.
 */
#ifndef QMC_METRIC_H
#define QMC_METRIC_H

#include <qmc.h>
#include <qmc_desc.h>
#include <qmc_group.h>
#include <qmc_context.h>

#include <qlist.h>
#include <qvector.h>
#include <qstring.h>
#include <qtextstream.h>

class QmcMetricValue;

class QmcEventRecord
{
public:
    QmcEventRecord() { my.missed = my.flags = 0; }

    void setTimestamp(struct timeval *tv) { my.timestamp = *tv; }
    void setMissed(int missed) { my.missed = missed; }
    void setFlags(int flags) { my.flags = flags; }

    int add(pmID pmid, QmcContext *cp, pmValueSet const *vp);

    static pmID eventFlags();
    static pmID eventMissed();

private:
    struct {
	struct timeval	timestamp;
	int		missed;
	int		flags;
	QVector<QmcMetricValue> parameters;
    } my;
};

class QmcMetricValue
{
public:
    QmcMetricValue();
    QmcMetricValue const& operator=(QmcMetricValue const& rhs);

    int instance() const { return my.instance; }
    void setInstance(int instance) { my.instance = instance; }

    int error() const { return my.error; }
    void setError(int error) { my.error = error; }
    void setAllErrors(int error)
	{ my.error = my.currentError = my.previousError = error; }

    double value() const { return my.value; }
    void setValue(double value) { my.value = value; }
    void divValue(double value) { my.value /= value; }
    void addValue(double value) { my.value += value; }
    void subValue(double value) { my.value -= value; }

    QString stringValue() const { return my.stringValue; }
    void setStringValue(const char *s) { my.stringValue = s; }

    QString eventValue() const { return QString::null; /* TODO */ }
    void setEventRecords(QVector<QmcEventRecord> &records) { my.eventRecords = records; }

    int currentError() const { return my.currentError; }
    void setCurrentError(int error)
	{ my.currentError = error; resetCurrentValue(); }
    double currentValue() const { return my.currentValue; }
    void setCurrentValue(double value) { my.currentValue = value; }

    int previousError() const { return my.previousError; }
    double previousValue() const { return my.previousValue; }
    void shiftValues() { my.previousValue = my.currentValue;
			 my.previousError = my.currentError;
			 my.currentError = 0; }

private:
    void resetCurrentValue()
	{ my.currentValue = 0.0; my.stringValue = QString::null; my.eventRecords.clear(); }

    struct {
	int instance;
	int error;
	double value;
	double previousValue;
	double currentValue;
	int currentError;
	int previousError;
	QString stringValue;
	QVector<QmcEventRecord> eventRecords;
    } my;
};

class QmcMetric
{
    friend class QmcGroup;
    friend class QmcContext;

public:
    QmcMetric(QmcGroup *group, const char *str, double theScale = 0.0,
	       bool active = false);
    QmcMetric(QmcGroup *group, pmMetricSpec *theMetric, double theScale = 0.0,
	       bool active = false);
    ~QmcMetric();

    int status() const { return my.status; }
    const QString name() const { return my.name; }
    const char *nameAscii() const { return (const char *)my.name.toAscii(); }
    QmcContext *context() const
	{ return my.group->context(my.contextIndex); }
    const QmcDesc &desc() const
	{ return context()->desc(my.pmid); }
    bool hasInstances() const
	{ return (my.status >= 0 && my.indomIndex < UINT_MAX); }

    // Were the instances explicitly listed?
    bool explicitInsts() const { return my.explicitInst; }

    // Are only active instances referenced
    bool activeInsts() const { return my.active; }

    int numInst() const
	{ return (my.status >= 0 && my.indomIndex < UINT_MAX) ?
	  my.values.size() : 0; }

    // How many values does it have (will not equal number of instances
    // if singular)
    int numValues() const { return (my.status >= 0) ? my.values.size() : 0; }

    // The metric indom
    QmcIndom *indom() const
	{ return (my.indomIndex == UINT_MAX) ? NULL :
		&(my.group->context(my.contextIndex)->indom(my.indomIndex)); }

    // Internal instance id for instance <index>
    int instID(int index) const
	{ return my.group->context(my.contextIndex)->indom(my.indomIndex).inst(my.values[index].instance()); }

    // External instance name for instance <index>
    const QString instName(int index) const
	{ return my.group->context(my.contextIndex)->indom(my.indomIndex).name(my.values[index].instance()); }

    // Return the index for the instance in the indom list
    int instIndex(uint index) const { return my.values[index].instance(); }

    // Update the metric to include new instances
    // Returns true if the instance list changed
    // Metrics with implicit instances will be extended to include those
    // new instances. The position of instances may change.
    // If <active> is set, only those instances in the latest indom will
    // be listed, other instances will be removed
    bool updateIndom();

    int addInst(QString const& name);
    void removeInst(uint index);

    // Scaling modifier applied to metric values
    double scale() const { return my.scale; }

    // Metric has event records (as opposed to real/string/aggregate values)
    bool event() const { return event(desc().desc().type); }
    static bool event(int type) { return type == PM_TYPE_EVENT; }

    // Metric has real values (as opposed to event/string/aggregate values)
    bool real() const { return real(desc().desc().type); }
    static bool real(int type)
	{ return type > PM_TYPE_NOSUPPORT && type < PM_TYPE_STRING; }

    // Current rate-converted and scaled real value
    double value(int index) const { return my.values[index].value(); }

    double realValue(int index) const		// Current rate-converted value
	{ return my.values[index].value() * my.scale; }

    double currentValue(int index) const	// Current raw value
	{ return my.values[index].currentValue(); }

    QString stringValue(int index) const	// Current string value
	{ return my.values[index].stringValue(); }

    QString eventValue(int index) const		// Current event records
	{ return my.values[index].eventValue(); }

    int error(int index) const	// Current error code (after rate-conversion)
	{ return my.values[index].error(); }

    int currentError(int index) const	// Current raw error code
	{ return my.values[index].currentError(); }

    void shiftValues();		// Shift values in preparation for next fetch

    void setError(int sts);	// Set error code for all instances

    void extractValues(pmValueSet const* set);	// Extract values after a fetch

    uint contextIndex() const	// Index for context in group list
	{ return my.contextIndex; }

    // Index for metric into pmResult
    uint idIndex() const { return my.idIndex; }

    // Index for indom in context list
    uint indomIndex() const { return my.indomIndex; }

    // Set the canonical units
    void setScaleUnits(pmUnits const& units);

    // Generate a metric spec
    QString spec(bool srcFlag = false,
		 bool instFlag = false,
		 uint instance = UINT_MAX) const;

    // Dump out the metric and its current value(s)
    void dump(QTextStream &os, bool srcFlag = false,
	      uint instance = UINT_MAX) const;

    // Dump out the current value
    void dumpValue(QTextStream &os, uint instance) const;

    // Dump out the metric source
    void dumpSource(QTextStream &os) const;

    // Format a value into a fixed width format
    static const char *formatNumber(double value);

    // Determine the current errors and rate-converted scaled values
    int update();

    friend QTextStream &operator<<(QTextStream &os, const QmcMetric &metric);

private:
    struct {
	pmID pmid;
	int status;
	QString name;
	QmcGroup *group;
	QList<QmcMetricValue> values;
	double scale;

	uint contextIndex;	// Index into the context list for the group
	uint idIndex;		// Index into the pmid list for the context.
	uint indomIndex;	// Index into the indom list for the context.

	bool explicitInst;	// Instances explicitly specified
	bool active;		// Use only active implicit insts
    } my;

    void setup(QmcGroup *group, pmMetricSpec *theMetric);
    void setupDesc(QmcGroup *group, pmMetricSpec *theMetric);
    void setupIndom(pmMetricSpec *theMetric);
    void setupValues(int num);

    void extractNumericMetric(pmValueSet const *vset, pmValue const *v, QmcMetricValue &vref);
    void extractArrayMetric(pmValueSet const *vset, pmValue const *v, QmcMetricValue &vref);
    void extractEventMetric(pmValueSet const *vset, int index, QmcMetricValue &vref);

    void setIdIndex(uint index) { my.idIndex = index; }

    // Dump error messages
    void dumpAll() const;
    void dumpErr() const;
    void dumpErr(const char *inst) const;
};

#endif	// QMC_METRIC_H